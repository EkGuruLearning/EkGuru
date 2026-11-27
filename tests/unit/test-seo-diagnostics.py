#!/usr/bin/env python3
"""Direct, offline regression fixtures for the two legacy SEO diagnostics.

Run: python3 -B tests/unit/test-seo-diagnostics.py
All HTML fixtures, reports and subprocess runs use disposable temporary roots.
No browser, network, generation or dependency installation is involved.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tests/regression" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PHASE6 = load("phase6_seo", "test-phase6-seo.py")
SCALE = load("phase7c_seo", "test-phase7c-seo-scale.py")
RELATIVE = "learn/hindi/basics/index.html"
CANONICAL = "https://ekguru.shop/learn/hindi/basics/"
DESCRIPTION = '<meta name="description" content="A real description">'
CANON = f'<link rel="canonical" href="{CANONICAL}">'


def html(description=DESCRIPTION, canonical=CANON, title="A unique title", body='<h1>Heading</h1><nav class="crumb">Path</nav>'):
    return f"<!doctype html><html><head><title>{title}</title>{description}{canonical}</head><body>{body}</body></html>"


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


class FixtureCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, relative, source):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")

    def phase6(self, source):
        self.put(RELATIVE, source)
        return PHASE6.audit(self.root, [RELATIVE], [])

    def cli(self, module, *args):
        return subprocess.run([sys.executable, "-B", module.__file__, "--root", str(self.root), *args],
                              capture_output=True, text=True, timeout=30)

    def all_phase6_pages(self):
        for index, relative in enumerate(PHASE6.PAGES):
            canonical = "https://ekguru.shop/" + relative.removesuffix("index.html")
            self.put(relative, html(f'<meta name="description" content="Description {index}">',
                                    f'<link rel="canonical" href="{canonical}">', f"Title {index}"))
        for relative in PHASE6.NOINDEX_PAGES:
            self.put(relative, "<meta content='follow, NOINDEX' name='ROBOTS'>")


class Phase6ParserTests(FixtureCase):
    def test_attribute_orders_quotes_whitespace_case_and_entities(self):
        variants = [
            (DESCRIPTION, CANON),
            ("<meta content='A real description' name='description'>", f"<link href='{CANONICAL}' rel='canonical'>"),
            ("<META\n CONTENT = 'A real description'\tNAME = ' DESCRIPTION ' />", f'<LINK\n HREF = "{CANONICAL}" REL = "CANONICAL" />'),
            ("<meta name=description content='A real description'>", f"<link rel='alternate canonical' href={CANONICAL}>"),
            ("<meta content='A &amp; B' name='description'>", CANON),
        ]
        for description, canonical in variants:
            with self.subTest(description=description, canonical=canonical):
                self.assertTrue(self.phase6(html(description, canonical))["pass"])
        self.assertEqual(PHASE6.SEOPage(variants[-1][0]).descriptions, ["A & B"])

    def test_missing_description_fails(self):
        result = self.phase6(html(description=""))
        self.assertFalse(result["pass"])
        self.assertIn(RELATIVE + ": no meta description", result["fails"])

    def test_missing_canonical_fails(self):
        result = self.phase6(html(canonical=""))
        self.assertFalse(result["pass"])
        self.assertIn(RELATIVE + ": no canonical", result["fails"])

    def test_empty_or_absent_values_fail(self):
        for tag in ['<meta name="description" content="">', '<meta name="description" content="  ">', '<meta name="description">']:
            with self.subTest(tag=tag):
                self.assertFalse(self.phase6(html(description=tag))["pass"])
        for tag in ['<link rel="canonical" href="">', '<link rel="canonical" href="  ">', '<link rel="canonical">']:
            with self.subTest(tag=tag):
                self.assertFalse(self.phase6(html(canonical=tag))["pass"])

    def test_duplicate_canonicals_fail_even_if_identical_or_empty(self):
        for extra in [CANON, '<link rel="canonical" href="">', '<link rel="canonical" href="https://ekguru.shop/other/">']:
            with self.subTest(extra=extra):
                result = self.phase6(html(canonical=CANON + extra))
                self.assertFalse(result["pass"])
                self.assertIn(RELATIVE + ": duplicate canonical elements", result["fails"])

    def test_duplicate_description_elements_fail(self):
        self.assertFalse(self.phase6(html(description=DESCRIPTION * 2))["pass"])

    def test_duplicate_metadata_across_pages_fails(self):
        other = "learn/hindi/other/index.html"
        self.put(RELATIVE, html())
        self.put(other, html(canonical='<link rel="canonical" href="https://ekguru.shop/learn/hindi/other/">'))
        result = PHASE6.audit(self.root, [RELATIVE, other], [])
        self.assertFalse(result["pass"])
        self.assertTrue(any("duplicate title" in f for f in result["fails"]))
        self.assertTrue(any("duplicate meta description" in f for f in result["fails"]))

    def test_comments_scripts_styles_templates_do_not_supply_metadata(self):
        for wrapper in ["<!--{}-->", "<script>{}</script>", "<style>{}</style>", "<template>{}</template>"]:
            with self.subTest(wrapper=wrapper):
                result = self.phase6(html(description=wrapper.format(DESCRIPTION), canonical=wrapper.format(CANON)))
                self.assertFalse(result["pass"])
                self.assertIn(RELATIVE + ": no meta description", result["fails"])
                self.assertIn(RELATIVE + ": no canonical", result["fails"])

    def test_malformed_unterminated_metadata_fails(self):
        self.assertFalse(self.phase6('<title>Title</title><meta name="description" content="unterminated')["pass"])

    def test_malformed_unclosed_title_fails(self):
        self.assertFalse(self.phase6('<title>Title' + DESCRIPTION + CANON + '<h1>Heading</h1>crumb')["pass"])

    def test_duplicate_attributes_fail(self):
        result = self.phase6(html(description='<meta name="description" NAME="description" content="A real description">'))
        self.assertFalse(result["pass"])
        self.assertTrue(any("duplicate attribute" in f for f in result["fails"]))

    def test_recoverable_html_does_not_require_xml_void_tag_closing(self):
        self.assertTrue(self.phase6(html().replace('</body></html>', ''))["pass"])

    def test_canonical_must_be_self_not_merely_same_suffix(self):
        for url in ['https://evil.invalid/learn/hindi/basics/', 'https://ekguru.shop/not-basics/',
                    CANONICAL + '?wrong=1', 'http://ekguru.shop/learn/hindi/basics/']:
            with self.subTest(url=url):
                self.assertFalse(self.phase6(html(canonical=f'<link rel="canonical" href="{url}">'))["pass"])
        self.assertTrue(self.phase6(html(canonical=f'<link rel="canonical" href="{CANONICAL.rstrip("/")}">'))["pass"])

    def test_canonical_scheme_and_host_case_are_not_path_case(self):
        self.assertTrue(self.phase6(html(canonical='<link rel="canonical" href="HTTPS://EKGURU.SHOP/learn/hindi/basics/">'))["pass"])
        self.assertFalse(self.phase6(html(canonical='<link rel="canonical" href="https://ekguru.shop/learn/HINDI/basics/">'))["pass"])

    def test_missing_title_still_fails(self):
        self.assertFalse(self.phase6(html(title=" "))["pass"])

    def test_h1_rule_still_fails(self):
        for body in ['<nav class="crumb">Path</nav>', '<h1>A</h1><h1>B</h1>crumb']:
            with self.subTest(body=body):
                self.assertFalse(self.phase6(html(body=body))["pass"])

    def test_breadcrumb_rule_still_fails(self):
        self.assertFalse(self.phase6(html(body='<h1>Heading</h1>'))["pass"])

    def test_download_rule_still_fails_but_honest_disclaimer_passes(self):
        self.assertFalse(self.phase6(html(body='<h1>Heading</h1>crumb <a>Download now</a>'))["pass"])
        self.assertTrue(self.phase6(html(body='<h1>Heading</h1>crumb No download buttons'))["pass"])

    def test_advertising_rule_still_fails(self):
        self.assertFalse(self.phase6(html(body='<h1>Heading</h1>crumb <script src="adsbygoogle.js"></script>'))["pass"])

    def test_noindex_tokens_case_and_order(self):
        self.put('review.html', "<META CONTENT='follow, NOINDEX' NAME='ROBOTS'>")
        self.assertTrue(PHASE6.audit(self.root, [], ['review.html'])["pass"])
        for source in ["<meta name='robots' content='index, follow'>", "<meta name='robots' content='noindexish'>", "<!--name=\"robots\" content=\"noindex\"-->"]:
            with self.subTest(source=source):
                self.put('review.html', source)
                self.assertFalse(PHASE6.audit(self.root, [], ['review.html'])["pass"])

    def test_missing_page_is_failure_not_crash(self):
        self.assertFalse(PHASE6.audit(self.root, [RELATIVE], ["missing-review.html"])["pass"])

    def test_cli_exit_codes_match_report_and_preserve_pages(self):
        self.all_phase6_pages()
        before = hashes(self.root)
        passed = self.cli(PHASE6)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        report = json.loads((self.root / 'reports/phase6-seo.json').read_text())
        self.assertTrue(report['pass'])
        self.put(RELATIVE, html(canonical=CANON * 2))
        failed = self.cli(PHASE6)
        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        self.assertFalse(json.loads((self.root / 'reports/phase6-seo.json').read_text())['pass'])
        after = hashes(self.root)
        self.assertEqual({k: v for k, v in after.items() if k in before and k != RELATIVE},
                         {k: v for k, v in before.items() if k != RELATIVE})
        self.assertEqual(set(after) - set(before), {'reports/phase6-seo.json'})


class ScaleGateTests(FixtureCase):
    def basic(self, body='<h1>Home</h1>'):
        self.put('index.html', html(canonical='<link rel="canonical" href="https://ekguru.shop/">', body=body))

    def test_valid_local_graph_passes_without_writes(self):
        self.basic('<a href="/other/">Other</a>')
        self.put('other/index.html', html(title="Other", description='<meta name="description" content="Other description">'))
        before = hashes(self.root)
        result = SCALE.audit(self.root)
        self.assertTrue(result['pass'])
        self.assertEqual(result['brokenInternalLinks']['count'], 0)
        self.assertEqual(hashes(self.root), before)

    def test_broken_internal_link_fails(self):
        self.basic('<a href="/missing/">Broken</a>')
        result = SCALE.audit(self.root)
        self.assertFalse(result['pass'])
        self.assertEqual(result['brokenInternalLinks']['count'], 1)
        self.assertTrue(any('required 0' in f for f in result['blockingFailures']))

    def test_single_quotes_uppercase_and_relative_links_checked(self):
        self.basic("<A HREF='missing.html?x=1#part'>Broken</A>")
        self.assertFalse(SCALE.audit(self.root)['pass'])

    def test_asset_extension_does_not_hide_broken_target(self):
        self.basic('<a href="/missing.pdf">PDF</a><a href="/missing.svg">SVG</a>')
        result = SCALE.audit(self.root)
        self.assertFalse(result['pass'])
        self.assertEqual(result['brokenInternalLinks']['count'], 2)
        self.put('missing.pdf', 'fixture asset')
        self.put('missing.svg', '<svg/>')
        self.assertTrue(SCALE.audit(self.root)['pass'])

    def test_external_urls_hashes_and_non_http_schemes_do_not_require_local_files(self):
        self.basic(''.join(f'<a href="{href}">Link</a>' for href in
                           ['https://external.invalid/nope', '//external.invalid/nope',
                            'https://ekguru.shop.evil.invalid/nope', 'mailto:test@example.invalid', 'tel:123', '#heading', 'javascript:void(0)']))
        self.assertTrue(SCALE.audit(self.root)['pass'])

    def test_same_origin_absolute_and_protocol_relative_links_are_checked(self):
        self.basic('<a href="https://ekguru.shop/missing/">A</a><a href="//ekguru.shop/also-missing/">B</a>')
        self.assertEqual(SCALE.audit(self.root)['brokenInternalLinks']['count'], 2)

    def test_script_style_comment_template_links_are_not_static_anchors(self):
        self.basic("<script>const s='<a href=\"/missing/\">';</script><style>/*<a href='/missing/'>*/</style><!--<a href='/missing/'>--><template><a href='/missing/'></a></template>")
        self.assertTrue(SCALE.audit(self.root)['pass'])

    def test_informational_only_metrics_do_not_become_arbitrary_gates(self):
        self.basic()
        self.put('other/index.html', html())
        self.put('third/index.html', html())
        result = SCALE.audit(self.root)
        self.assertTrue(result['pass'])
        self.assertEqual(result['blockingFailures'], [])
        self.assertGreater(result['duplicateTitles']['count'], 0)
        self.assertGreater(result['duplicateDescriptions']['count'], 0)
        self.assertGreater(result['canonicalDrift']['count'], 0)
        self.assertGreater(result['orphanPages']['count'], 0)
        self.assertIn('canonicalDrift', result['informationalMetrics'])

    def test_missing_metadata_is_reported_without_inventing_global_threshold(self):
        self.put('index.html', '<h1>Home</h1>')
        result = SCALE.audit(self.root)
        self.assertTrue(result['pass'])
        self.assertEqual(result['metadataObservations']['missingTitles'], 1)
        self.assertEqual(result['metadataObservations']['missingDescriptions'], 1)

    def test_robots_attribute_order_case_and_none_are_measured(self):
        self.put('index.html', "<meta content='NOINDEX, follow' NAME='robots'>")
        self.put('other/index.html', "<meta name='robots' content='none'>")
        result = SCALE.audit(self.root)
        self.assertEqual((result['indexable'], result['noindex']), (0, 2))

    def test_legacy_tutor_alias_is_informational_not_automatic_failure(self):
        self.basic()
        self.put('tutor.html', html(canonical='<link rel="canonical" href="https://ekguru.shop/tutor/">'))
        result = SCALE.audit(self.root)
        self.assertTrue(result['pass'])
        self.assertEqual(result['canonicalDrift']['intentionalLegacyAliases'], [('/tutor.html', 'https://ekguru.shop/tutor/')])

    def test_empty_or_missing_root_fails(self):
        self.assertFalse(SCALE.audit(self.root)['pass'])
        self.assertFalse(SCALE.audit(self.root / 'missing')['pass'])

    def test_unreadable_discovered_page_fails(self):
        self.basic()
        with patch.object(Path, 'read_text', side_effect=OSError('fixture read failure')):
            result = SCALE.audit(self.root)
        self.assertFalse(result['pass'])
        self.assertEqual(result['pagesRead'], 0)
        self.assertTrue(any('unreadable page' in f for f in result['blockingFailures']))

    def test_url_encoded_paths_and_extensionless_fallbacks(self):
        self.basic('<a href="/with%20space/">Space</a><a href="/standalone">Standalone</a>')
        self.put('with space/index.html', html())
        self.put('standalone.html', html())
        self.assertTrue(SCALE.audit(self.root)['pass'])

    def test_cli_pass_fail_and_informational_exit_codes(self):
        self.basic()
        passed = self.cli(SCALE)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        report = self.root / 'reports/global-seo-scale-phase7c.json'
        self.assertTrue(json.loads(report.read_text())['pass'])
        self.put('other/index.html', html())
        informational = self.cli(SCALE)
        self.assertEqual(informational.returncode, 0, informational.stdout + informational.stderr)
        self.assertGreater(json.loads(report.read_text())['duplicateTitles']['count'], 0)
        self.basic('<a href="/missing/">Broken</a>')
        failed = self.cli(SCALE)
        self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
        self.assertIn('FAIL', failed.stdout)
        self.assertFalse(json.loads(report.read_text())['pass'])


class ReportSafetyTests(FixtureCase):
    def test_import_has_no_chdir_or_report_side_effects(self):
        before_cwd = Path.cwd()
        before = hashes(self.root)
        for index, filename in enumerate(['test-phase6-seo.py', 'test-phase7c-seo-scale.py']):
            load('import_safety_' + str(index), filename)
        self.assertEqual(Path.cwd(), before_cwd)
        self.assertEqual(hashes(self.root), before)

    def test_no_report_mode_is_read_only(self):
        self.all_phase6_pages()
        self.put('index.html', html())
        before = hashes(self.root)
        for module in [PHASE6, SCALE]:
            result = self.cli(module, '--no-report')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(hashes(self.root), before)

    def test_only_fixed_private_reports_are_written(self):
        self.all_phase6_pages()
        self.put('index.html', html())
        before = hashes(self.root)
        for module in [PHASE6, SCALE]:
            result = self.cli(module)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = hashes(self.root)
        self.assertEqual(set(after) - set(before), {'reports/phase6-seo.json', 'reports/global-seo-scale-phase7c.json'})
        self.assertEqual({k: after[k] for k in before}, before)

    def test_symlinked_report_file_cannot_overwrite_public_html(self):
        self.put('index.html', 'must remain unchanged')
        (self.root / 'reports').mkdir()
        for module, name in [(PHASE6, 'phase6-seo.json'), (SCALE, 'global-seo-scale-phase7c.json')]:
            (self.root / 'reports' / name).symlink_to(self.root / 'index.html')
            with self.assertRaises(OSError):
                module.write_report(self.root, {'pass': True})
        self.assertEqual((self.root / 'index.html').read_text(), 'must remain unchanged')

    def test_symlinked_report_directory_is_rejected(self):
        (self.root / 'public').mkdir()
        (self.root / 'reports').symlink_to(self.root / 'public', target_is_directory=True)
        for module in [PHASE6, SCALE]:
            with self.assertRaises(OSError):
                module.write_report(self.root, {'pass': True})
        self.assertEqual(list((self.root / 'public').iterdir()), [])

    def test_report_io_failure_has_nonzero_exit_and_fail_marker(self):
        self.all_phase6_pages()
        self.put('reports', 'not a directory')
        for module in [PHASE6, SCALE]:
            result = self.cli(module)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn('FAIL', result.stdout)


class TextContextTests(FixtureCase):
    """Focused fixtures for RCDATA, raw text and plaintext; originals above intact."""

    PAYLOAD = DESCRIPTION + CANON + '<a href="/fake-context-target/">Fake</a>'
    CONTEXTS = ('textarea', 'title', 'xmp', 'iframe', 'noembed', 'noframes')

    def test_textarea_cannot_supply_description(self):
        result = self.phase6(html(description='', body='<h1>H</h1>crumb<textarea>' + DESCRIPTION + '</textarea>'))
        self.assertFalse(result['pass'])
        self.assertIn(RELATIVE + ': no meta description', result['fails'])

    def test_textarea_cannot_supply_canonical(self):
        result = self.phase6(html(canonical='', body='<h1>H</h1>crumb<textarea>' + CANON + '</textarea>'))
        self.assertFalse(result['pass'])
        self.assertIn(RELATIVE + ': no canonical', result['fails'])

    def test_textarea_cannot_supply_anchor(self):
        page = SCALE.PageInfo('<textarea><a href="/fake/">Text</a></textarea>')
        self.assertEqual(page.links, set())

    def test_all_text_contexts_ignore_fake_metadata_and_links(self):
        for tag in self.CONTEXTS:
            source = f'<{tag}>Text {self.PAYLOAD}</{tag}>'
            for parser in [PHASE6.SEOPage, SCALE.PageInfo]:
                with self.subTest(tag=tag, parser=parser.__name__):
                    page = parser(source)
                    self.assertEqual(page.descriptions, [])
                    self.assertEqual(page.canonicals, [])
                    if parser is SCALE.PageInfo:
                        self.assertEqual(page.links, set())

    def test_title_keeps_literal_markup_and_decodes_entities_once(self):
        literal = ('Example &lt;/title&gt; &lt;meta name="description" content="encoded"&gt; '
                   '<meta name="description" content="fake"> <a href="/fake/">Link</a> &amp; &amp;lt;')
        expected = ('Example </title> <meta name="description" content="encoded"> '
                    '<meta name="description" content="fake"> <a href="/fake/">Link</a> & &lt;')
        page6 = PHASE6.SEOPage('<title>' + literal + '</title>')
        page7 = SCALE.PageInfo('<title>' + literal + '</title>')
        self.assertEqual(page6.titles, [expected])
        self.assertEqual(page6.errors, [])
        self.assertEqual(page7.title, expected)
        self.assertEqual(page7.links, set())
        self.assertEqual(page6.descriptions, [])
        self.assertEqual(page7.descriptions, [])

    def test_genuine_elements_after_matching_end_tag_survive(self):
        for tag in self.CONTEXTS:
            # Only title provides the real title itself; do not create two titles.
            title = '' if tag == 'title' else '<title>Real title</title>'
            source = (f'<{tag}>Literal {self.PAYLOAD}</{tag}>' + title + DESCRIPTION + CANON
                      + '<h1>Real heading</h1>crumb<a href="/real/">Real</a>')
            with self.subTest(tag=tag):
                page6, page7 = PHASE6.SEOPage(source), SCALE.PageInfo(source)
                self.assertEqual(page6.descriptions, ['A real description'])
                self.assertEqual(page6.canonicals, [CANONICAL])
                self.assertEqual(len(page6.titles), 1)
                self.assertEqual(page6.h1_count, 1)
                self.assertEqual(page6.errors, [])
                self.assertEqual(page7.descriptions, ['A real description'])
                self.assertEqual(page7.canonicals, [CANONICAL])
                self.assertEqual(page7.links, {'/real/'})
                self.assertTrue(self.phase6(source)['pass'])

    def test_missing_real_metadata_still_fails_for_every_context(self):
        for tag in self.CONTEXTS:
            title = '' if tag == 'title' else '<title>Real title</title>'
            with self.subTest(tag=tag):
                result = self.phase6(title + f'<{tag}>{self.PAYLOAD}</{tag}><h1>H</h1>crumb')
                self.assertFalse(result['pass'])
                self.assertIn(RELATIVE + ': no meta description', result['fails'])
                self.assertIn(RELATIVE + ': no canonical', result['fails'])

    def test_real_duplicate_metadata_still_fails_outside_context(self):
        source = html(description=DESCRIPTION * 2, canonical=CANON * 2,
                      body='<h1>H</h1>crumb<textarea>' + self.PAYLOAD + '</textarea>')
        result = self.phase6(source)
        self.assertFalse(result['pass'])
        self.assertIn(RELATIVE + ': multiple meta description elements', result['fails'])
        self.assertIn(RELATIVE + ': duplicate canonical elements', result['fails'])

    def test_fake_headings_and_robots_are_not_real_elements(self):
        for tag in self.CONTEXTS:
            source = f'<{tag}><h1>Fake</h1><meta name="robots" content="noindex"></{tag}>'
            with self.subTest(tag=tag):
                self.assertEqual(PHASE6.SEOPage(source).h1_count, 0)
                self.assertEqual(PHASE6.SEOPage(source).robots, [])
                self.assertEqual(SCALE.PageInfo(source).robots, [])

    def test_nonvoid_self_closing_looking_openings_still_enter_text(self):
        for tag in self.CONTEXTS:
            for opening in [f'<{tag}/>', f'<{tag} />']:
                with self.subTest(opening=opening):
                    source = opening + self.PAYLOAD + f'</{tag}>' + DESCRIPTION + CANON + '<a href="/real/">Real</a>'
                    for parser in [PHASE6.SEOPage, SCALE.PageInfo]:
                        page = parser(source)
                        self.assertEqual(page.descriptions, ['A real description'])
                        self.assertEqual(page.canonicals, [CANONICAL])
                        if parser is SCALE.PageInfo:
                            self.assertEqual(page.links, {'/real/'})
        self.assertEqual(PHASE6.SEOPage('<title/>Real &amp; title</title>').titles, ['Real & title'])

    def test_mixed_case_matching_end_tags_and_ascii_whitespace(self):
        for tag in self.CONTEXTS:
            with self.subTest(tag=tag):
                source = f'<{tag.upper()}>{self.PAYLOAD}</{tag.upper()} \t\n>' + DESCRIPTION
                self.assertEqual(PHASE6.SEOPage(source).descriptions, ['A real description'])
                self.assertEqual(SCALE.PageInfo(source).descriptions, ['A real description'])

    def test_misleading_end_tags_do_not_end_text(self):
        for tag in self.CONTEXTS:
            for ending in [f'</{tag}suffix>', f'</{tag}-suffix>', f'</ {tag}>', f'</{tag}\v>']:
                with self.subTest(tag=tag, ending=ending):
                    source = f'<{tag}>' + ending + self.PAYLOAD + f'</{tag}>' + DESCRIPTION
                    self.assertEqual(PHASE6.SEOPage(source).descriptions, ['A real description'])
                    page = SCALE.PageInfo(source)
                    self.assertEqual(page.descriptions, ['A real description'])
                    self.assertEqual(page.links, set())

    def test_quoted_end_tag_attributes_do_not_expose_fake_markup(self):
        for tag in self.CONTEXTS:
            with self.subTest(tag=tag):
                source = f'<{tag}>Text</{tag} data-note=\'>{self.PAYLOAD}\'>' + DESCRIPTION
                for parser in [PHASE6.SEOPage, SCALE.PageInfo]:
                    page = parser(source)
                    self.assertEqual(page.descriptions, ['A real description'])
                    self.assertEqual(page.canonicals, [])
                    if parser is SCALE.PageInfo:
                        self.assertEqual(page.links, set())

    def test_unclosed_contexts_never_retokenize_eof_text(self):
        for tag in self.CONTEXTS:
            with self.subTest(tag=tag):
                source = f'<{tag}>Text {self.PAYLOAD}'
                page6, page7 = PHASE6.SEOPage(source), SCALE.PageInfo(source)
                self.assertEqual(page6.descriptions, [])
                self.assertEqual(page6.canonicals, [])
                self.assertEqual(page7.descriptions, [])
                self.assertEqual(page7.canonicals, [])
                self.assertEqual(page7.links, set())
                if tag == 'title':
                    self.assertIn('unclosed title element', page6.errors)
                    self.assertEqual(page6.titles, [])
                    self.assertIn(self.PAYLOAD, page7.title)

    def test_plaintext_remains_raw_through_eof_even_after_fake_end_tag(self):
        for opening in ['<plaintext>', '<plaintext/>']:
            source = '<title>Real</title>' + opening + self.PAYLOAD + '</plaintext>' + self.PAYLOAD
            for parser in [PHASE6.SEOPage, SCALE.PageInfo]:
                with self.subTest(opening=opening, parser=parser.__name__):
                    page = parser(source)
                    self.assertEqual(page.descriptions, [])
                    self.assertEqual(page.canonicals, [])
                    if parser is SCALE.PageInfo:
                        self.assertEqual(page.title, 'Real')
                        self.assertEqual(page.links, set())

    def test_rcdata_and_rawtext_character_reference_semantics_differ(self):
        for module in [PHASE6, SCALE]:
            class Recorder(module.HTMLTextParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.text = []

                def handle_text(self, data):
                    self.text.append(data)

            for tag in self.CONTEXTS + ('script', 'style', 'plaintext'):
                with self.subTest(module=module.__name__, tag=tag):
                    content = '&lt;meta&gt; &amp;lt; &#65; &amp;'
                    source = f'<{tag}>{content}' + (f'</{tag}>' if tag != 'plaintext' else '')
                    recorder = Recorder()
                    recorder.feed(source)
                    recorder.close()
                    expected = '<meta> &lt; A &' if tag in ('title', 'textarea') else content
                    self.assertEqual(''.join(recorder.text), expected)

    def test_incremental_feeds_preserve_end_tag_and_entity_boundaries(self):
        for module in [PHASE6, SCALE]:
            class Recorder(module.HTMLTextParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.events = []

                def handle_text(self, data):
                    self.events.append(('text', data))

                def handle_starttag(self, tag, attrs):
                    self.events.append(('start', tag))

            for tag in ('title', 'textarea', 'xmp'):
                recorder = Recorder()
                for fragment in [f'<{tag}', '/>A &am', 'p;lt;<meta name="fake">', f'</{tag.upper()}', '><a href="/real/">']:
                    recorder.feed(fragment)
                recorder.close()
                with self.subTest(module=module.__name__, tag=tag):
                    self.assertEqual([value for kind, value in recorder.events if kind == 'start'], [tag, 'a'])
                    expected = 'A &lt;<meta name="fake">' if tag != 'xmp' else 'A &amp;lt;<meta name="fake">'
                    self.assertEqual(''.join(value for kind, value in recorder.events if kind == 'text'), expected)

    def test_noscript_and_ordinary_containers_keep_real_fallback_markup(self):
        for tag in ('noscript', 'pre', 'code'):
            with self.subTest(tag=tag):
                source = f'<{tag}>' + DESCRIPTION + CANON + '<a href="/real/">Real</a>' + f'</{tag}>'
                self.assertEqual(PHASE6.SEOPage(source).descriptions, ['A real description'])
                page = SCALE.PageInfo(source)
                self.assertEqual(page.canonicals, [CANONICAL])
                self.assertEqual(page.links, {'/real/'})

    def test_encoded_markup_in_normal_text_is_never_reparsed(self):
        source = '&lt;meta name="description" content="fake"&gt;&lt;a href="/fake/"&gt;'
        self.assertEqual(PHASE6.SEOPage(source).descriptions, [])
        self.assertEqual(SCALE.PageInfo(source).links, set())

    def test_actual_link_gate_ignores_fake_but_blocks_real_missing_target(self):
        self.put('index.html', html(body='<textarea><a href="/fake/">Fake</a></textarea>'))
        self.assertTrue(SCALE.audit(self.root)['pass'])
        self.put('index.html', html(body='<textarea><a href="/fake/">Fake</a></textarea><a href="/real-missing/">Real</a>'))
        result = SCALE.audit(self.root)
        self.assertFalse(result['pass'])
        self.assertEqual(result['brokenInternalLinks']['count'], 1)
        self.assertEqual(result['brokenInternalLinks']['examples'], [('/', '/real-missing/')])

    def test_text_adapter_copies_remain_identical(self):
        import ast
        adapters = []
        for module in (PHASE6, SCALE):
            source = Path(module.__file__).read_text()
            node = next(node for node in ast.parse(source).body
                        if isinstance(node, ast.ClassDef) and node.name == 'HTMLTextParser')
            adapters.append(ast.get_source_segment(source, node))
        self.assertEqual(adapters[0], adapters[1])


if __name__ == '__main__':
    unittest.main()

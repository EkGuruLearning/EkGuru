#!/usr/bin/env python3
"""Offline regression tests for crawl-target and shell relocation checks."""
import unittest
import runpy
from pathlib import Path

from pathlib import Path as _RepoPath
import sys as _repo_sys
_repo_sys.path.insert(0, str(_RepoPath(__file__).resolve().parents[2] / 'tools'))
from discovery_integrity import Page, audit, prefix_relative_references, public_target


class DiscoveryTests(unittest.TestCase):
    def test_relocate_real_attributes_only(self):
        raw = '''<link href="css/style.min.css"><a href='learn/hindi/?q=a&amp;b=c#lesson'>Go</a>
<script src="js/main.js"></script><script>var example = '<a href="not-a-link">';</script>
<style>.x:after{content:'href="not-a-link"'}</style><!-- <a href="comment"> -->
<img src="/images/logo.svg"><a href="../contact/">Contact</a><a href="#faq">FAQ</a>
<a href="https://example.com/">External</a><source src="media.mp3"/>'''
        out = prefix_relative_references(raw)
        self.assertIn('href="../css/style.min.css"', out)
        self.assertIn("href='../learn/hindi/?q=a&amp;b=c#lesson'", out)
        self.assertIn('src="../js/main.js"', out)
        self.assertIn('src="../media.mp3"', out)
        self.assertIn("var example = '<a href=\"not-a-link\">'", out)
        self.assertIn('href="../contact/"', out)
        self.assertNotIn('../../contact/', out)
        self.assertIn('href="https://example.com/"', out)
        self.assertEqual(prefix_relative_references(out), out)

    def test_encoded_and_query_urls(self):
        files = {"index.html", "a b/index.html", "search/index.html", "image.png"}
        self.assertEqual(public_target("https://ekguru.shop/a%20b/?x=1#top", files), "a b/index.html")
        self.assertEqual(public_target("https://ekguru.shop/search/?q=test", files), "search/index.html")
        self.assertEqual(public_target("https://ekguru.shop/image.png", files), "image.png")
        self.assertEqual(public_target("https://ekguru.shop/missing/", files), "")
        self.assertIsNone(public_target("https://example.com/", files))

    def test_private_files_and_absolute_same_site_links_fail(self):
        pages = {"index.html": Page('<a href="https://ekguru.shop/tools/private.py">Private</a><script src="/missing.js"></script>')}
        errors, count = audit({"index.html"}, pages)
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 2)

    def test_base_url_and_script_literals(self):
        pages = {"a/index.html": Page('<base href="/"><a href="contact/">Contact</a><script>var a=\'<a href="missing">\';</script>')}
        errors, count = audit({"a/index.html", "contact/index.html"}, pages)
        self.assertEqual((errors, count), ([], 1))

    def test_nonreciprocal_and_noncanonical_alternates_fail(self):
        pages = {
            "index.html": Page('<link rel="alternate" hreflang="es" href="https://ekguru.shop/es/">'),
            "es/index.html": Page('<link rel="canonical" href="https://ekguru.shop/other/">'),
        }
        errors, _ = audit(set(pages), pages)
        self.assertTrue(any("return link" in error for error in errors))
        self.assertTrue(any("self-canonical" in error for error in errors))

    def test_reciprocal_alternates(self):
        links = '<link rel="alternate" hreflang="en" href="https://ekguru.shop/"><link rel="alternate" hreflang="es" href="https://ekguru.shop/es/">'
        pages = {
            "index.html": Page('<link rel="canonical" href="https://ekguru.shop/">' + links),
            "es/index.html": Page('<link rel="canonical" href="https://ekguru.shop/es/">' + links),
        }
        self.assertEqual(audit(set(pages), pages)[0], [])


class LiveGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = runpy.run_path(str((Path(__file__).resolve().parents[2] / "tools/live-seo-gate.py")))

    def response(self, status=200, body=None, **headers):
        return {"status": status, "url": "https://ekguru.shop/", "headers": {"content-type": "text/html", **headers},
                "body": body if body is not None else '<html><head><title>EkGuru</title><link rel="canonical" href="https://ekguru.shop/"></head><body><h1>Learn Hindi</h1></body></html>'}

    def test_healthy_page_and_headers(self):
        self.assertEqual(self.gate["page_errors"](self.response(), "https://ekguru.shop/"), [])
        errors = self.gate["page_errors"](self.response(**{"x-robots-tag": "googlebot: noindex"}), "https://ekguru.shop/")
        self.assertTrue(any("noindex" in error for error in errors))

    def test_challenges_and_network_errors_never_pass(self):
        self.assertTrue(self.gate["response_errors"](self.response(**{"cf-mitigated": "challenge"})))
        self.assertTrue(self.gate["response_errors"](self.response(status=0)))
        self.assertTrue(self.gate["response_errors"](self.response(status=503)))

    def test_empty_sitemaps_and_wrong_hosts_fail(self):
        for body in ['<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>',
                     '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://example.com/sitemap.xml</loc></sitemap></sitemapindex>']:
            self.assertTrue(self.gate["sitemap_locs"](self.response(body=body), "sitemapindex")[1])

    def test_soft_404_and_invisible_content_fail(self):
        self.assertTrue(self.gate["response_errors"](self.response(), 404))
        blank = '<head><title>EkGuru</title><link rel="canonical" href="https://ekguru.shop/"></head><body></body>'
        self.assertIn("missing visible H1", self.gate["page_errors"](self.response(body=blank), "https://ekguru.shop/"))


if __name__ == "__main__":
    unittest.main()

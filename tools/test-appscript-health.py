#!/usr/bin/env python3
"""Unit tests for honest Apps Script health-probe classification."""

from io import BytesIO
from pathlib import Path
import sys
import unittest
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.appscript_health import is_unverified_appscript_403


class AppScriptHealthProbeTests(unittest.TestCase):
    def http_error(self, status):
        return HTTPError(
            "https://script.google.com/macros/s/example/exec",
            status,
            "HTTP response",
            {},
            BytesIO(b""),
        )

    def test_403_is_unverified_not_a_health_pass(self):
        self.assertTrue(is_unverified_appscript_403(self.http_error(403)))

    def test_other_http_errors_remain_failures(self):
        for status in (401, 404, 429, 500):
            with self.subTest(status=status):
                self.assertFalse(is_unverified_appscript_403(self.http_error(status)))

    def test_network_error_remains_a_failure(self):
        self.assertFalse(is_unverified_appscript_403(URLError("offline")))


if __name__ == "__main__":
    unittest.main(verbosity=2)

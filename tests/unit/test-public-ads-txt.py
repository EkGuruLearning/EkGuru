#!/usr/bin/env python3
"""Deployment guard fixtures; this is not a live Google crawler test."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('public_dist',ROOT/'tools/build-public-dist.py')
D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)


class AdsTxtArtifact(unittest.TestCase):
    def test_root_file_required_and_correct(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            self.assertTrue(D.check_ads_txt(folder))
            (root/'nested').mkdir();(root/'nested/ads.txt').write_bytes((ROOT/'ads.txt').read_bytes())
            self.assertTrue(D.check_ads_txt(folder))
            (root/'ads.txt').write_bytes((ROOT/'ads.txt').read_bytes())
            self.assertFalse(D.check_ads_txt(folder))

    def test_html_wrong_id_and_duplicate_record_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'ads.txt'
            record='google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0'
            for text in ['<html>Not found</html>',record.replace('8175326569491671','0000000000000000'),record+'\n'+record,'']:
                p.write_text(text);self.assertTrue(D.check_ads_txt(folder),text)
            p.write_text('# comment\r\n'+record+'\r\n');self.assertFalse(D.check_ads_txt(folder))


if __name__=='__main__':unittest.main()

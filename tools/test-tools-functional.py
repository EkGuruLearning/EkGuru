#!/usr/bin/env python3
"""Compatibility entrypoint only; canonical test: tests/regression/test-tools-functional.py. No test assertions live here."""
from pathlib import Path
import subprocess
import sys
raise SystemExit(subprocess.call([sys.executable, str(Path(__file__).resolve().parents[1] / 'tests/regression/test-tools-functional.py'), *sys.argv[1:]]))

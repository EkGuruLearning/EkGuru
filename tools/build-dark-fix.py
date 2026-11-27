#!/usr/bin/env python3
"""Compatibility entrypoint; canonical implementation: tools/pipeline/assets/build-dark-fix.py.

Execute in this module's own namespace so functions use its mutable globals.
ROOT and CWD semantics belong to the canonical implementation, not this adapter.
"""
from pathlib import Path as _ek_Path

_ek_legacy_file = __file__
_ek_canonical_file = _ek_Path(__file__).resolve().parent / "pipeline" / "assets" / "build-dark-fix.py"
try:
    __file__ = str(_ek_canonical_file)
    exec(
        compile(_ek_canonical_file.read_bytes(), __file__, "exec", dont_inherit=True),
        globals(),
        globals(),
    )
finally:
    __file__ = _ek_legacy_file
    del _ek_Path, _ek_canonical_file, _ek_legacy_file

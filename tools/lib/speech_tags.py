# -*- coding: utf-8 -*-
"""Canonical BCP-47 speech tags for the published languages.

A speech tag is a request for a device voice, never a promise that a device has
one. The region subtag matters: browsers match ``ja-JP`` and ``ko-KR`` against
installed voices, while a fabricated ``ja-JA`` or ``ko-KO`` matches nothing and
silently falls back to the default voice — so a wrong tag is a real defect that
no schema can catch, only this table.

``speech_tag()`` falls back to the **bare language code** (``xx``), which is
valid BCP-47, instead of inventing a region by uppercasing the code. The old
``code + "-" + code.upper()`` pattern wrote ``ja-JA``, ``ko-KO``, ``uk-UK`` and
``vi-VI`` into ``data/language-packs.json`` and from there into the registry,
``js/voice-languages.js`` and every page that inlines it.
"""
from __future__ import annotations

#: Languages the site publishes a course or a starter pack for. Extend this
#: table when a language is added; never let a caller guess the region.
SPEECH_TAGS = {
    "ar": "ar-SA", "bn": "bn-IN", "de": "de-DE", "en": "en-IN", "es": "es-ES",
    "fa": "fa-IR", "fr": "fr-FR", "gu": "gu-IN", "he": "he-IL", "hi": "hi-IN",
    "id": "id-ID", "it": "it-IT", "ja": "ja-JP", "kn": "kn-IN", "ko": "ko-KR",
    "ml": "ml-IN", "ms": "ms-MY", "mr": "mr-IN", "nl": "nl-NL", "pa": "pa-IN",
    "pl": "pl-PL", "pt": "pt-BR", "ru": "ru-RU", "sw": "sw-KE", "ta": "ta-IN",
    "te": "te-IN", "th": "th-TH", "tr": "tr-TR", "uk": "uk-UA", "ur": "ur-PK",
    "vi": "vi-VN", "zh": "zh-CN",
}


def speech_tag(code: str) -> str:
    """Return the canonical speech tag for ``code`` (bare code when unknown)."""
    return SPEECH_TAGS.get(code) or code


__all__ = ["SPEECH_TAGS", "speech_tag"]

"""Simple LibreTranslate wrapper for Chinese/English translation."""
from __future__ import annotations

import os
from typing import Literal, Optional

import requests

TranslateDirection = Literal["en2zh", "zh2en"]

DEFAULT_TRANSLATE_URL = os.getenv("LIBRE_TRANSLATE_URL") or "https://translate.argosopentech.com/translate"


class TranslationError(RuntimeError):
    """Raised when the translation service fails."""


def translate_text(text: str, direction: TranslateDirection, url: Optional[str] = None) -> str:
    """Translate text between English and Chinese using LibreTranslate-compatible APIs."""

    target_url = (url or DEFAULT_TRANSLATE_URL).rstrip("/")
    source_lang, target_lang = ("en", "zh") if direction == "en2zh" else ("zh", "en")

    response = requests.post(
        target_url,
        json={
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
        },
        timeout=15,
    )
    if response.status_code >= 400:
        raise TranslationError(f"Translation failed with status {response.status_code}: {response.text}")

    data = response.json()
    translated = data.get("translatedText")
    if not translated:
        raise TranslationError("Translation response missing 'translatedText' field")
    return translated


__all__ = ["translate_text", "TranslateDirection", "TranslationError"]

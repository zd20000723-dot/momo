"""Client helper for interacting with the MoMo (墨墨背单词) API.

The API details are intentionally flexible. Configure the base URL and
authentication token via environment variables or CLI options.
"""
from __future__ import annotations

import os
from typing import Iterable, List, Optional

import requests


class MoMoClient:
    """Lightweight HTTP client for retrieving MoMo word data."""

    def __init__(
        self,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        daily_endpoint: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("MOMO_API_BASE") or "https://api.maimemo.com").rstrip(
            "/"
        )
        self.daily_endpoint = (
            daily_endpoint
            or os.getenv("MOMO_DAILY_ENDPOINT")
            or "/v2/review/today-words"
        )
        self.session = session or requests.Session()
        self.token = token or os.getenv("MOMO_API_TOKEN")
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def fetch_today_words(self) -> List[str]:
        """Fetch today's review words.

        The endpoint defaults to ``/v2/review/today-words`` but can be overridden
        via ``daily_endpoint`` or the ``MOMO_DAILY_ENDPOINT`` environment variable.
        """

        url = self._build_url(self.daily_endpoint)
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return self._extract_words(data)

    def fetch_words_for_date(self, date: str) -> List[str]:
        """Fetch words for a specific date string (e.g. ``2024-06-01``).

        The path is resolved relative to ``base_url``; customize it via
        ``MOMO_DATE_ENDPOINT`` when the API differs.
        """

        endpoint = os.getenv("MOMO_DATE_ENDPOINT") or "/v2/review/words-by-date"
        url = self._build_url(endpoint)
        response = self.session.get(url, params={"date": date}, timeout=10)
        response.raise_for_status()
        data = response.json()
        return self._extract_words(data)

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    def _extract_words(self, payload: object) -> List[str]:
        words: List[str] = []

        if isinstance(payload, dict):
            candidate = payload.get("data") or payload.get("words")
            if candidate:
                return self._extract_words(candidate)
            maybe_word = payload.get("word") or payload.get("content")
            if isinstance(maybe_word, str):
                words.append(maybe_word)
        elif isinstance(payload, list):
            for item in payload:
                words.extend(self._extract_words(item))
        elif isinstance(payload, str):
            words.append(payload)

        return words


__all__ = ["MoMoClient"]

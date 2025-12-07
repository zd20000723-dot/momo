"""Official-style MoMo (墨墨背单词) Open API helper.

This client follows the开放平台文档（https://open.maimemo.com）提供的典型流程：

1. 使用 ``client_id`` 与 ``client_secret`` 请求 ``access_token``。
2. 在带 ``Bearer`` 认证的情况下调用单词查询接口。

所有路径均可通过参数或环境变量调整，方便对齐最新文档。
"""
from __future__ import annotations

import os
from typing import List, Optional

import requests


class MoMoClient:
    """Lightweight HTTP client that mirrors the官方开放平台接口。"""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        base_url: Optional[str] = None,
        token_endpoint: Optional[str] = None,
        today_endpoint: Optional[str] = None,
        dated_endpoint: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("MOMO_API_BASE") or "https://open.maimemo.com").rstrip("/")
        self.token_endpoint = token_endpoint or os.getenv("MOMO_TOKEN_ENDPOINT") or "/oauth2/token"
        self.today_endpoint = today_endpoint or os.getenv("MOMO_TODAY_ENDPOINT") or "/api/v1/memo-words/today-review"
        self.dated_endpoint = dated_endpoint or os.getenv("MOMO_DATED_ENDPOINT") or "/api/v1/memo-words/review-by-date"

        self.client_id = client_id or os.getenv("MOMO_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("MOMO_CLIENT_SECRET")
        self.session = session or requests.Session()
        self.access_token = access_token or os.getenv("MOMO_ACCESS_TOKEN")

    def fetch_today_words(self) -> List[str]:
        """Fetch today's review words via官方接口路径。"""

        url = self._build_url(self.today_endpoint)
        response = self._get(url)
        data = response.json()
        return self._extract_words(data)

    def fetch_words_for_date(self, date: str) -> List[str]:
        """Fetch review words for a specific ``YYYY-MM-DD`` date."""

        url = self._build_url(self.dated_endpoint)
        response = self._get(url, params={"date": date})
        data = response.json()
        return self._extract_words(data)

    # Internals -----------------------------------------------------------------
    def _ensure_token(self) -> str:
        if self.access_token:
            return self.access_token
        if not self.client_id or not self.client_secret:
            raise ValueError("MoMo client_id/client_secret 未配置，无法获取 access_token。")

        url = self._build_url(self.token_endpoint)
        response = self.session.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise RuntimeError("未在 MoMo token 响应中找到 access_token 字段。")
        self.access_token = token
        return token

    def _get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        token = self._ensure_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response

    def _build_url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path if path.startswith('/') else '/' + path}"

    def _extract_words(self, payload: object) -> List[str]:
        """Accepts official payloads such as ``{"data": [{"word": "apple"}]}``."""

        words: List[str] = []

        if isinstance(payload, dict):
            candidate = payload.get("data") or payload.get("words")
            if candidate is not None:
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

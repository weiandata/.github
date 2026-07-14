"""Small redacting GitHub REST API client using only the Python standard library."""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any


RETRYABLE_STATUSES = frozenset({429, 502, 503, 504})


class GitHubClient:
    """GitHub REST client with bounded retry and credential-safe logging."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://api.github.com",
        opener: Callable[..., Any] = urllib.request.urlopen,
        sleep: Callable[[float], None] = time.sleep,
        logger: logging.Logger | None = None,
    ) -> None:
        if not token:
            raise ValueError("GitHub token must not be empty")
        self._token = token
        self._base_url = base_url.rstrip("/")
        self._opener = opener
        self._sleep = sleep
        self._logger = logger or logging.getLogger(__name__)

    def _redact(self, value: str) -> str:
        return value.replace(self._token, "[REDACTED]")

    @staticmethod
    def _retry_delay(error: urllib.error.HTTPError, retry_index: int) -> float:
        retry_after = error.headers.get("Retry-After") if error.headers else None
        if retry_after:
            try:
                return max(0, int(retry_after))
            except ValueError:
                pass
        return float(2**retry_index)

    def request(self, method: str, path: str, body: Any = None) -> Any:
        """Make one JSON API request, retrying transient failures at most three times."""

        if not path.startswith("/"):
            raise ValueError("GitHub API path must start with '/'")
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "weiandata-waef-governance",
        }
        data = None
        if body is not None:
            data = json.dumps(body, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(
            f"{self._base_url}{path}", data=data, headers=headers, method=method.upper()
        )
        for attempt in range(4):
            try:
                with self._opener(request) as response:
                    payload = response.read()
                    return json.loads(payload) if payload else None
            except urllib.error.HTTPError as error:
                try:
                    response_body = error.read().decode("utf-8", errors="replace")
                finally:
                    error.close()
                self._logger.warning(
                    "GitHub API %s %s returned %s: %s",
                    method.upper(),
                    path,
                    error.code,
                    self._redact(response_body),
                )
                if error.code not in RETRYABLE_STATUSES or attempt == 3:
                    raise
                self._sleep(self._retry_delay(error, attempt))

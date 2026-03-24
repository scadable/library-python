from __future__ import annotations

import time
from typing import Any

import httpx

from .._config import ClientConfig
from .._exceptions import ConnectionError, from_response
from ._base import Response


class SyncHTTPTransport:
    def __init__(self, config: ClientConfig):
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={"Authorization": f"Bearer {config.api_key}"},
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        last_exc: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                resp = self._client.request(method, path, json=json, params=params)
            except httpx.HTTPError as exc:  # pragma: no cover
                last_exc = exc  # pragma: no cover
                if attempt < self._config.max_retries:  # pragma: no cover
                    time.sleep(min(2**attempt, 8))  # pragma: no cover
                    continue  # pragma: no cover
                raise ConnectionError(str(exc)) from exc  # pragma: no cover

            if resp.status_code == 429 or resp.status_code >= 500:
                last_exc = from_response(resp.status_code, _safe_json(resp))
                if attempt < self._config.max_retries:
                    time.sleep(min(2**attempt, 8))
                    continue

            if resp.status_code >= 400:
                raise from_response(resp.status_code, _safe_json(resp))

            return Response(
                status_code=resp.status_code,
                data=_safe_json(resp),
                headers=dict(resp.headers),
            )

        raise last_exc or ConnectionError(
            "Request failed after retries"
        )  # pragma: no cover

    def close(self) -> None:
        self._client.close()


class AsyncHTTPTransport:
    def __init__(self, config: ClientConfig):
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={"Authorization": f"Bearer {config.api_key}"},
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response:
        import asyncio

        last_exc: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                resp = await self._client.request(
                    method, path, json=json, params=params
                )
            except httpx.HTTPError as exc:  # pragma: no cover
                last_exc = exc  # pragma: no cover
                if attempt < self._config.max_retries:  # pragma: no cover
                    await asyncio.sleep(min(2**attempt, 8))  # pragma: no cover
                    continue  # pragma: no cover
                raise ConnectionError(str(exc)) from exc  # pragma: no cover

            if resp.status_code == 429 or resp.status_code >= 500:
                last_exc = from_response(resp.status_code, _safe_json(resp))
                if attempt < self._config.max_retries:
                    await asyncio.sleep(min(2**attempt, 8))
                    continue

            if resp.status_code >= 400:
                raise from_response(resp.status_code, _safe_json(resp))

            return Response(
                status_code=resp.status_code,
                data=_safe_json(resp),
                headers=dict(resp.headers),
            )

        raise last_exc or ConnectionError(
            "Request failed after retries"
        )  # pragma: no cover

    async def close(self) -> None:
        await self._client.aclose()


def _safe_json(resp: httpx.Response) -> dict[str, Any] | None:
    try:
        return resp.json()
    except Exception:
        return None

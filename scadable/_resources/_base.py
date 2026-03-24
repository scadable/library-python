from __future__ import annotations

from typing import Any, TypeVar, Type

from pydantic import BaseModel

from .._transport._base import Response

T = TypeVar("T", bound=BaseModel)


def _extract_list(data: Any) -> list[Any]:
    """Extract a list from an API response — handles raw arrays, wrapped objects, etc."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Find the first list value in the dict (e.g. {"gateways": [...], "total": 2})
        for value in data.values():
            if isinstance(value, list):
                return value
        # Single object — wrap it
        return [data]
    return []


class SyncResource:
    def __init__(self, transport: Any):
        self._transport = transport

    def _get(
        self, path: str, *, model: Type[T], params: dict[str, Any] | None = None
    ) -> T:
        resp: Response = self._transport.request("GET", path, params=params)
        return model.model_validate(resp.data)

    def _list(
        self, path: str, *, model: Type[T], params: dict[str, Any] | None = None
    ) -> list[T]:
        resp: Response = self._transport.request("GET", path, params=params)
        return [model.model_validate(item) for item in _extract_list(resp.data)]


class AsyncResource:
    def __init__(self, transport: Any):
        self._transport = transport

    async def _get(
        self, path: str, *, model: Type[T], params: dict[str, Any] | None = None
    ) -> T:
        resp: Response = await self._transport.request("GET", path, params=params)
        return model.model_validate(resp.data)

    async def _list(
        self, path: str, *, model: Type[T], params: dict[str, Any] | None = None
    ) -> list[T]:
        resp: Response = await self._transport.request("GET", path, params=params)
        return [model.model_validate(item) for item in _extract_list(resp.data)]

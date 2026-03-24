from __future__ import annotations

from typing import Any, TypeVar, Type

from pydantic import BaseModel

from .._transport._base import Response

T = TypeVar("T", bound=BaseModel)


class SyncResource:
    def __init__(self, transport: Any):
        self._transport = transport

    def _get(self, path: str, *, model: Type[T], params: dict[str, Any] | None = None) -> T:
        resp: Response = self._transport.request("GET", path, params=params)
        return model.model_validate(resp.data)

    def _list(self, path: str, *, model: Type[T], params: dict[str, Any] | None = None) -> list[T]:
        resp: Response = self._transport.request("GET", path, params=params)
        data = resp.data
        # Handle both raw arrays and wrapped responses
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # Try common wrapper keys
            for key in ("data", "items", "results", "gateways", "projects", "tasks"):
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            else:
                items = [data]
        else:
            items = []
        return [model.model_validate(item) for item in items]


class AsyncResource:
    def __init__(self, transport: Any):
        self._transport = transport

    async def _get(self, path: str, *, model: Type[T], params: dict[str, Any] | None = None) -> T:
        resp: Response = await self._transport.request("GET", path, params=params)
        return model.model_validate(resp.data)

    async def _list(self, path: str, *, model: Type[T], params: dict[str, Any] | None = None) -> list[T]:
        resp: Response = await self._transport.request("GET", path, params=params)
        data = resp.data
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ("data", "items", "results", "gateways", "projects", "tasks"):
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            else:
                items = [data]
        else:
            items = []
        return [model.model_validate(item) for item in items]

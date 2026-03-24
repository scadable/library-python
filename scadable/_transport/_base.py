from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Protocol, runtime_checkable


@dataclass
class Response:
    status_code: int
    data: Any
    headers: dict[str, str]


@runtime_checkable
class Transport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response: ...

    def close(self) -> None: ...


@runtime_checkable
class AsyncTransport(Protocol):
    async def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Response: ...

    async def close(self) -> None: ...


@runtime_checkable
class StreamTransport(Protocol):
    """Persistent bidirectional stream (WebSocket today, WebRTC later)."""

    def connect(self, path: str) -> AsyncIterator[dict[str, Any]]: ...

    async def close(self) -> None: ...

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

import websockets
from websockets.asyncio.client import connect

from .._config import ClientConfig


class WebSocketTransport:
    def __init__(self, config: ClientConfig):
        self._config = config

    @asynccontextmanager
    async def connect(self, path: str) -> AsyncIterator[AsyncIterator[dict[str, Any]]]:
        base = self._config.base_url.replace("https://", "wss://").replace("http://", "ws://")
        url = f"{base}{path}?token={self._config.api_key}"

        async with connect(url) as ws:
            async def _iter() -> AsyncIterator[dict[str, Any]]:
                async for raw in ws:
                    try:
                        yield json.loads(raw)
                    except json.JSONDecodeError:
                        continue

            yield _iter()

    async def close(self) -> None:
        pass

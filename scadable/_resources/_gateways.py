from __future__ import annotations

from typing import Any, AsyncIterator
from contextlib import asynccontextmanager

from .._models._gateway import Gateway, Device
from .._models._telemetry import TelemetryEvent
from ._base import SyncResource, AsyncResource


class Gateways(SyncResource):
    def list(self) -> list[Gateway]:
        return self._list("/v1/gateways", model=Gateway)

    def get(self, gateway_id: str) -> Gateway:
        return self._get(f"/v1/gateways/{gateway_id}", model=Gateway)

    def devices(self, gateway_id: str) -> list[Device]:
        return self._list(f"/v1/gateways/{gateway_id}/devices", model=Device)


class AsyncGateways(AsyncResource):
    def __init__(self, transport: Any, stream_transport: Any = None):
        super().__init__(transport)
        self._stream_transport = stream_transport

    async def list(self) -> list[Gateway]:
        return await self._list("/v1/gateways", model=Gateway)

    async def get(self, gateway_id: str) -> Gateway:
        return await self._get(f"/v1/gateways/{gateway_id}", model=Gateway)

    async def devices(self, gateway_id: str) -> list[Device]:
        return await self._list(f"/v1/gateways/{gateway_id}/devices", model=Device)

    @asynccontextmanager
    async def stream(
        self, gateway_id: str
    ) -> AsyncIterator[AsyncIterator[TelemetryEvent]]:
        if not self._stream_transport:
            raise RuntimeError("Streaming requires AsyncScadable client")
        path = f"/v1/gateways/{gateway_id}/stream"  # pragma: no cover
        async with self._stream_transport.connect(
            path
        ) as raw_stream:  # pragma: no cover

            async def _parse() -> AsyncIterator[TelemetryEvent]:  # pragma: no cover
                async for msg in raw_stream:
                    yield TelemetryEvent.model_validate(msg)

            yield _parse()  # pragma: no cover

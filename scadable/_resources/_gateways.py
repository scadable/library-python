from __future__ import annotations

from typing import Any, AsyncIterator
from contextlib import asynccontextmanager

from .._models._gateway import Gateway, GatewayMetrics, GatewaySecurity
from .._models._telemetry import TelemetryEvent
from ._base import SyncResource, AsyncResource


class Gateways(SyncResource):
    def list(self, *, project_id: str) -> list[Gateway]:
        return self._list(f"/api/projects/{project_id}/gateways", model=Gateway)

    def get(self, *, project_id: str, gateway_id: str) -> Gateway:
        return self._get(f"/api/projects/{project_id}/gateways/{gateway_id}", model=Gateway)

    def metrics(self, *, project_id: str, gateway_id: str, range: str = "1h") -> GatewayMetrics:
        return self._get(
            f"/api/projects/{project_id}/gateways/{gateway_id}/metrics",
            model=GatewayMetrics,
            params={"range": range},
        )

    def security(self, *, project_id: str, gateway_id: str) -> GatewaySecurity:
        return self._get(
            f"/api/projects/{project_id}/gateways/{gateway_id}/security",
            model=GatewaySecurity,
        )


class AsyncGateways(AsyncResource):
    def __init__(self, transport: Any, stream_transport: Any = None):
        super().__init__(transport)
        self._stream_transport = stream_transport

    async def list(self, *, project_id: str) -> list[Gateway]:
        return await self._list(f"/api/projects/{project_id}/gateways", model=Gateway)

    async def get(self, *, project_id: str, gateway_id: str) -> Gateway:
        return await self._get(f"/api/projects/{project_id}/gateways/{gateway_id}", model=Gateway)

    async def metrics(self, *, project_id: str, gateway_id: str, range: str = "1h") -> GatewayMetrics:
        return await self._get(
            f"/api/projects/{project_id}/gateways/{gateway_id}/metrics",
            model=GatewayMetrics,
            params={"range": range},
        )

    async def security(self, *, project_id: str, gateway_id: str) -> GatewaySecurity:
        return await self._get(
            f"/api/projects/{project_id}/gateways/{gateway_id}/security",
            model=GatewaySecurity,
        )

    @asynccontextmanager
    async def stream(self, *, project_id: str, gateway_id: str) -> AsyncIterator[AsyncIterator[TelemetryEvent]]:
        if not self._stream_transport:
            raise RuntimeError("Streaming requires AsyncScadable client")
        path = f"/api/projects/{project_id}/gateways/{gateway_id}/ws"
        async with self._stream_transport.connect(path) as raw_stream:
            async def _parse() -> AsyncIterator[TelemetryEvent]:
                async for msg in raw_stream:
                    yield TelemetryEvent.model_validate(msg)
            yield _parse()

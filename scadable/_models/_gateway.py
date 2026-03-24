from __future__ import annotations

from datetime import datetime
from typing import Any

from ._base import ScadableModel


class Device(ScadableModel):
    device_id: str | None = None
    id: str | None = None
    name: str | None = None
    status: str | None = None
    protocol: str | None = None
    connected: bool | None = None
    gateway_id: str | None = None
    last_seen_at: datetime | None = None
    last_error: str | None = None


class Gateway(ScadableModel):
    id: str | None = None
    gateway_id: str | None = None
    name: str
    status: str = "unknown"
    firmware_version: str | None = None
    version: str | None = None
    project_id: str | None = None
    os: str | None = None
    arch: str | None = None
    last_seen_at: datetime | None = None
    created_at: datetime | None = None
    devices: list[Device] = []
    uptime_percent_30d: float | None = None
    uptime_percent_7d: float | None = None


class MetricPoint(ScadableModel):
    timestamp: float
    value: float


class GatewayMetrics(ScadableModel):
    gateway_id: str | None = None
    range: str | None = None
    cpu: list[MetricPoint] = []
    memory: list[MetricPoint] = []
    outbound_bytes: list[MetricPoint] = []


class GatewaySecurity(ScadableModel):
    gateway_firmware: str | None = None
    kernel: str | None = None
    os_release: str | None = None
    package_count: int = 0
    packages: dict[str, Any] = {}
    vulnerability_summary: dict[str, int] = {}
    drivers: dict[str, str] = {}
    scanned_at: datetime | None = None

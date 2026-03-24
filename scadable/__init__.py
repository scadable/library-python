"""Scadable Python SDK — the simplest way to interact with the Scadable IoT platform."""

from ._client import Scadable, AsyncScadable
from ._config import ClientConfig
from ._exceptions import (
    ScadableError,
    AuthenticationError,
    ConnectionError,
    InternalServerError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from ._models import (
    Device,
    Gateway,
    GatewayMetrics,
    GatewaySecurity,
    MetricPoint,
    TelemetryEvent,
)

__all__ = [
    "Scadable",
    "AsyncScadable",
    "ClientConfig",
    # Errors
    "ScadableError",
    "AuthenticationError",
    "ConnectionError",
    "InternalServerError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
    # Models
    "Device",
    "Gateway",
    "GatewayMetrics",
    "GatewaySecurity",
    "MetricPoint",
    "TelemetryEvent",
]

__version__ = "2.0.2"

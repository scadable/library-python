from __future__ import annotations

from typing import Any

from ._base import ScadableModel


class TelemetryEvent(ScadableModel):
    type: str
    data: dict[str, Any] = {}
    task_id: str | None = None

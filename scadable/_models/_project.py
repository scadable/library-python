from __future__ import annotations

from datetime import datetime

from ._base import ScadableModel


class Project(ScadableModel):
    id: str
    name: str
    description: str | None = None
    owner_email: str | None = None
    created_at: datetime | None = None
    members_count: int | None = None

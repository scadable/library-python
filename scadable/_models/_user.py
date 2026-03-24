from __future__ import annotations

from ._base import ScadableModel


class User(ScadableModel):
    email: str
    name: str | None = None
    picture: str | None = None
    user_id: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    company: str | None = None
    role: str | None = None

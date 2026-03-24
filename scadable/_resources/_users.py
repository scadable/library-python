from __future__ import annotations

from .._models._user import User
from ._base import SyncResource, AsyncResource


class Users(SyncResource):
    def me(self) -> User:
        return self._get("/api/me", model=User)


class AsyncUsers(AsyncResource):
    async def me(self) -> User:
        return await self._get("/api/me", model=User)

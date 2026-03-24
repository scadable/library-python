from __future__ import annotations

from .._models._project import Project
from ._base import SyncResource, AsyncResource


class Projects(SyncResource):
    def list(self) -> list[Project]:
        return self._list("/api/projects", model=Project)

    def get(self, *, project_id: str) -> Project:
        return self._get(f"/api/projects/{project_id}", model=Project)


class AsyncProjects(AsyncResource):
    async def list(self) -> list[Project]:
        return await self._list("/api/projects", model=Project)

    async def get(self, *, project_id: str) -> Project:
        return await self._get(f"/api/projects/{project_id}", model=Project)

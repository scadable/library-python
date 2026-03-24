import pytest
import respx
from httpx import Response

from scadable import AsyncScadable, Gateway, Project, User


@pytest.mark.asyncio
async def test_async_list_projects(mock_api):
    mock_api.get("/api/projects").mock(
        return_value=Response(200, json=[{"id": "p1", "name": "Proj"}])
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        projects = await client.projects.list()
        assert len(projects) == 1
        assert isinstance(projects[0], Project)


@pytest.mark.asyncio
async def test_async_get_project(mock_api):
    mock_api.get("/api/projects/p1").mock(
        return_value=Response(200, json={"id": "p1", "name": "Proj"})
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        project = await client.projects.get(project_id="p1")
        assert project.id == "p1"


@pytest.mark.asyncio
async def test_async_me(mock_api):
    mock_api.get("/api/me").mock(
        return_value=Response(200, json={"email": "a@b.com", "name": "Ali"})
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        user = await client.users.me()
        assert isinstance(user, User)
        assert user.email == "a@b.com"


@pytest.mark.asyncio
async def test_async_list_gateways(mock_api):
    mock_api.get("/api/projects/p1/gateways").mock(
        return_value=Response(
            200, json=[{"id": "gw1", "name": "Pi", "status": "online"}]
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gws = await client.gateways.list(project_id="p1")
        assert len(gws) == 1
        assert isinstance(gws[0], Gateway)


@pytest.mark.asyncio
async def test_async_get_gateway(mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1").mock(
        return_value=Response(
            200, json={"id": "gw1", "name": "Pi", "status": "online", "devices": []}
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gw = await client.gateways.get(project_id="p1", gateway_id="gw1")
        assert gw.name == "Pi"


@pytest.mark.asyncio
async def test_async_gateway_metrics(mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1/metrics").mock(
        return_value=Response(
            200,
            json={
                "gateway_id": "gw1",
                "range": "1h",
                "cpu": [{"timestamp": 1700000000, "value": 10.0}],
                "memory": [],
                "outbound_bytes": [],
            },
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        m = await client.gateways.metrics(project_id="p1", gateway_id="gw1")
        assert len(m.cpu) == 1


@pytest.mark.asyncio
async def test_async_gateway_security(mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1/security").mock(
        return_value=Response(
            200,
            json={"package_count": 42, "vulnerability_summary": {}, "drivers": {}},
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        sec = await client.gateways.security(project_id="p1", gateway_id="gw1")
        assert sec.package_count == 42

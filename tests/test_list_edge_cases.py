"""Test edge cases for _list parsing — wrapped responses, single objects, empty."""

import pytest
from httpx import Response

from scadable import AsyncScadable, Gateway, Project


def test_list_wrapped_response(client, mock_api):
    """API returns {"data": [...]} instead of raw array."""
    mock_api.get("/api/projects").mock(
        return_value=Response(
            200,
            json={"data": [{"id": "p1", "name": "Wrapped"}]},
        )
    )
    projects = client.projects.list()
    assert len(projects) == 1
    assert projects[0].name == "Wrapped"


def test_list_single_object_response(client, mock_api):
    """API returns a single object instead of array — wraps it in list."""
    mock_api.get("/api/projects").mock(
        return_value=Response(200, json={"id": "p1", "name": "Single"})
    )
    projects = client.projects.list()
    assert len(projects) == 1
    assert projects[0].name == "Single"


def test_list_null_response(client, mock_api):
    """API returns null/empty — returns empty list."""
    mock_api.get("/api/projects").mock(return_value=Response(200, json=None))
    projects = client.projects.list()
    assert projects == []


@pytest.mark.asyncio
async def test_async_list_wrapped(mock_api):
    mock_api.get("/api/projects").mock(
        return_value=Response(
            200,
            json={"data": [{"id": "p1", "name": "Wrapped"}]},
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        projects = await client.projects.list()
        assert len(projects) == 1


@pytest.mark.asyncio
async def test_async_list_single_object(mock_api):
    mock_api.get("/api/projects").mock(
        return_value=Response(200, json={"id": "p1", "name": "Single"})
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        projects = await client.projects.list()
        assert len(projects) == 1


@pytest.mark.asyncio
async def test_async_list_null(mock_api):
    mock_api.get("/api/projects").mock(return_value=Response(200, json=None))
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        projects = await client.projects.list()
        assert projects == []

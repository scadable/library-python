"""Test edge cases for _list parsing — wrapped responses, single objects, empty."""

import pytest
from httpx import Response

from scadable import AsyncScadable, Gateway


def test_list_raw_array(client, mock_api):
    """API returns a raw JSON array."""
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200,
            json=[{"gateway_id": "gw1", "name": "Raw", "status": "online"}],
        )
    )
    gateways = client.gateways.list()
    assert len(gateways) == 1
    assert gateways[0].name == "Raw"


def test_list_wrapped_response(client, mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200,
            json={
                "gateways": [
                    {"gateway_id": "gw1", "name": "Wrapped", "status": "online"}
                ]
            },
        )
    )
    gateways = client.gateways.list()
    assert len(gateways) == 1
    assert gateways[0].name == "Wrapped"


def test_list_single_object_response(client, mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200, json={"gateway_id": "gw1", "name": "Single", "status": "online"}
        )
    )
    gateways = client.gateways.list()
    assert len(gateways) == 1
    assert gateways[0].name == "Single"


def test_list_null_response(client, mock_api):
    mock_api.get("/v1/gateways").mock(return_value=Response(200, json=None))
    gateways = client.gateways.list()
    assert gateways == []


@pytest.mark.asyncio
async def test_async_list_wrapped(mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200,
            json={
                "gateways": [
                    {"gateway_id": "gw1", "name": "Wrapped", "status": "online"}
                ]
            },
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gateways = await client.gateways.list()
        assert len(gateways) == 1


@pytest.mark.asyncio
async def test_async_list_single_object(mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200, json={"gateway_id": "gw1", "name": "Single", "status": "online"}
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gateways = await client.gateways.list()
        assert len(gateways) == 1


@pytest.mark.asyncio
async def test_async_list_null(mock_api):
    mock_api.get("/v1/gateways").mock(return_value=Response(200, json=None))
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gateways = await client.gateways.list()
        assert gateways == []

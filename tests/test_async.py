import pytest
from httpx import Response

from scadable import AsyncScadable, Gateway, Device


@pytest.mark.asyncio
async def test_async_list_gateways(mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200,
            json={
                "gateways": [{"gateway_id": "gw1", "name": "Pi", "status": "online"}]
            },
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gws = await client.gateways.list()
        assert len(gws) == 1
        assert isinstance(gws[0], Gateway)


@pytest.mark.asyncio
async def test_async_get_gateway(mock_api):
    mock_api.get("/v1/gateways/gw1").mock(
        return_value=Response(
            200,
            json={"gateway_id": "gw1", "name": "Pi", "status": "online"},
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        gw = await client.gateways.get("gw1")
        assert gw.name == "Pi"


@pytest.mark.asyncio
async def test_async_list_devices(mock_api):
    mock_api.get("/v1/gateways/gw1/devices").mock(
        return_value=Response(
            200,
            json={"devices": [{"id": "d1", "name": "Sensor", "status": "connected"}]},
        )
    )
    async with AsyncScadable(
        api_key="sk_test", base_url="https://test.scadable.com"
    ) as client:
        devices = await client.gateways.devices("gw1")
        assert len(devices) == 1
        assert isinstance(devices[0], Device)

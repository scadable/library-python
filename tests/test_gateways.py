from httpx import Response

from scadable import Gateway, Device


def test_list_gateways(client, mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(
            200,
            json={
                "gateways": [
                    {"gateway_id": "gw1", "name": "Pi 5", "status": "online"},
                    {"gateway_id": "gw2", "name": "Pi 4", "status": "offline"},
                ],
                "total": 2,
            },
        )
    )

    gateways = client.gateways.list()
    assert len(gateways) == 2
    assert isinstance(gateways[0], Gateway)
    assert gateways[0].name == "Pi 5"
    assert gateways[0].status == "online"
    assert gateways[1].status == "offline"


def test_get_gateway(client, mock_api):
    mock_api.get("/v1/gateways/gw1").mock(
        return_value=Response(
            200,
            json={
                "gateway_id": "gw1",
                "name": "Pi 5",
                "status": "online",
                "firmware_version": "0.6.5",
            },
        )
    )

    gw = client.gateways.get("gw1")
    assert isinstance(gw, Gateway)
    assert gw.name == "Pi 5"


def test_list_devices(client, mock_api):
    mock_api.get("/v1/gateways/gw1/devices").mock(
        return_value=Response(
            200,
            json={
                "devices": [
                    {
                        "id": "d1",
                        "name": "Modbus Sensor",
                        "status": "connected",
                        "protocol": "modbus",
                    },
                ]
            },
        )
    )

    devices = client.gateways.devices("gw1")
    assert len(devices) == 1
    assert isinstance(devices[0], Device)
    assert devices[0].name == "Modbus Sensor"

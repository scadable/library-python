from httpx import Response

from scadable import Gateway, GatewayMetrics, GatewaySecurity


def test_list_gateways(client, mock_api):
    mock_api.get("/api/projects/p1/gateways").mock(
        return_value=Response(
            200,
            json=[
                {"id": "gw1", "name": "Pi 5", "status": "online", "version": "0.6.5"},
                {"id": "gw2", "name": "Pi 4", "status": "offline"},
            ],
        )
    )

    gateways = client.gateways.list(project_id="p1")
    assert len(gateways) == 2
    assert isinstance(gateways[0], Gateway)
    assert gateways[0].name == "Pi 5"
    assert gateways[0].status == "online"
    assert gateways[1].status == "offline"


def test_get_gateway(client, mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1").mock(
        return_value=Response(
            200,
            json={
                "id": "gw1",
                "gateway_id": "gw1",
                "name": "Pi 5",
                "status": "online",
                "version": "0.6.5",
                "os": "linux",
                "arch": "arm64",
                "devices": [
                    {
                        "id": "d1",
                        "name": "Modbus Sensor",
                        "status": "connected",
                        "protocol": "modbus",
                    },
                ],
            },
        )
    )

    gw = client.gateways.get(project_id="p1", gateway_id="gw1")
    assert isinstance(gw, Gateway)
    assert gw.name == "Pi 5"
    assert len(gw.devices) == 1
    assert gw.devices[0].name == "Modbus Sensor"


def test_gateway_metrics(client, mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1/metrics").mock(
        return_value=Response(
            200,
            json={
                "gateway_id": "gw1",
                "range": "1h",
                "cpu": [{"timestamp": 1700000000, "value": 12.5}],
                "memory": [{"timestamp": 1700000000, "value": 43.2}],
                "outbound_bytes": [{"timestamp": 1700000000, "value": 1024}],
            },
        )
    )

    metrics = client.gateways.metrics(project_id="p1", gateway_id="gw1")
    assert isinstance(metrics, GatewayMetrics)
    assert len(metrics.cpu) == 1
    assert metrics.cpu[0].value == 12.5


def test_gateway_security(client, mock_api):
    mock_api.get("/api/projects/p1/gateways/gw1/security").mock(
        return_value=Response(
            200,
            json={
                "gateway_firmware": "0.6.5",
                "kernel": "6.1.0",
                "package_count": 150,
                "vulnerability_summary": {
                    "critical": 0,
                    "high": 2,
                    "medium": 5,
                    "low": 10,
                },
                "drivers": {"modbus": "0.3.1"},
            },
        )
    )

    sec = client.gateways.security(project_id="p1", gateway_id="gw1")
    assert isinstance(sec, GatewaySecurity)
    assert sec.package_count == 150
    assert sec.vulnerability_summary["high"] == 2
    assert sec.drivers["modbus"] == "0.3.1"

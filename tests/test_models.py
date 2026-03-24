from scadable import Gateway, Device, Project, User, GatewayMetrics, MetricPoint


def test_gateway_extra_fields_ignored():
    """SDK should not break when API adds new fields."""
    gw = Gateway.model_validate(
        {
            "id": "gw1",
            "name": "Test",
            "status": "online",
            "some_future_field": "new value",
            "another_new_thing": 42,
        }
    )
    assert gw.id == "gw1"
    assert gw.name == "Test"


def test_gateway_with_devices():
    gw = Gateway.model_validate(
        {
            "id": "gw1",
            "name": "Test",
            "status": "online",
            "devices": [
                {"id": "d1", "name": "Sensor", "status": "connected"},
                {
                    "id": "d2",
                    "name": "PLC",
                    "status": "disconnected",
                    "protocol": "modbus",
                },
            ],
        }
    )
    assert len(gw.devices) == 2
    assert isinstance(gw.devices[0], Device)
    assert gw.devices[1].protocol == "modbus"


def test_gateway_defaults():
    gw = Gateway.model_validate({"id": "gw1", "name": "Minimal"})
    assert gw.status == "unknown"
    assert gw.devices == []
    assert gw.version is None


def test_project_minimal():
    p = Project.model_validate({"id": "p1", "name": "Test"})
    assert p.id == "p1"
    assert p.description is None


def test_user_minimal():
    u = User.model_validate({"email": "a@b.com"})
    assert u.email == "a@b.com"
    assert u.name is None


def test_metric_point():
    mp = MetricPoint.model_validate({"timestamp": 1700000000.0, "value": 42.5})
    assert mp.timestamp == 1700000000.0
    assert mp.value == 42.5

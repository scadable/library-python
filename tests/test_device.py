import pytest
from scadable.device import DeviceManager, Device
from .mock_connection import *


@pytest.fixture(scope="function")
def connection_factory():
    factory = TestConnectionFactory()
    return factory


@pytest.fixture(scope="function")
def device_manager():
    manager = DeviceManager()
    return manager


def test_device_manager_create_device(device_manager):
    # Creates a new device
    d1 = device_manager.create_device("abc", None)
    assert isinstance(d1, Device)
    assert len(device_manager.devices) == 1

    # Test to see if same device id returns the same
    d2 = device_manager.create_device("abc", None)
    assert d1 == d2
    assert len(device_manager.devices) == 1


def test_device_manager_get_device(device_manager):
    d1 = device_manager.create_device("abc", None)
    d2 = device_manager["abc"]

    assert d1 == d2


def test_device_manager_remove_device(device_manager):
    # Creates a new device
    d1 = device_manager.create_device("abc", None)

    device_manager.remove_device(d1.device_id)
    assert len(device_manager.devices) == 0


@pytest.mark.asyncio
async def test_device_raw_telemetry(connection_factory, device_manager):
    conn = connection_factory.create_connection("apikey", "abc")
    device = device_manager.create_device("abc", conn)

    messages = []

    # Basic Decorator Usage
    @device.raw_live_telemetry
    async def handle(m):
        messages.append(m)

    await device.start_live_telemetry()
    await device.connection.send_message("test")

    assert messages == ["test"]


@pytest.mark.asyncio
async def test_device_parsed_telemetry(connection_factory, device_manager):
    conn = connection_factory.create_connection("apikey", "abc")
    device = device_manager.create_device("abc", conn)

    messages = []

    # Basic Decorator Usage
    @device.live_telemetry
    async def handle(m):
        messages.append(m)

    await device.start_live_telemetry()
    await device.connection.send_message("test")

    assert messages == ["test"]


@pytest.mark.asyncio
async def test_device_no_conn(device_manager):
    device = device_manager.create_device("abc", None)

    messages = []

    with pytest.raises(RuntimeError):
        @device.raw_live_telemetry
        async def handle(m):
            messages.append(m)

    with pytest.raises(RuntimeError):
        @device.live_telemetry
        async def handle(m):
            messages.append(m)

    with pytest.raises(RuntimeError):
        await device.start_live_telemetry()

import pytest
from src.scadable.live_query.connection_type import ConnectionFactory, Connection
from src.scadable.live_query import DeviceFactory


class TestConnectionFactory(ConnectionFactory):
    def create_connection(self, device_id: str):
        return TestConnection()


class TestConnection(Connection):
    def __init__(self):
        super().__init__()
        self.handler = None

    async def connect(self, handler):
        self.handler = handler

    async def send_message(self, message):
        if self.handler:
            await self.handler(message)

    async def stop(self):
        pass


@pytest.mark.asyncio
async def test_device_factory():
    device_factory = DeviceFactory("apikey", TestConnectionFactory())
    assert device_factory.api_key == "apikey"
    device = device_factory.create_device("deviceid")
    assert isinstance(device.connection, TestConnection)


@pytest.mark.asyncio
async def test_device_connection():
    device_factory = DeviceFactory("apikey", TestConnectionFactory())
    device = device_factory.create_device("deviceid")

    messages = []

    # Basic Decorator Usage
    @device.raw_live_telemetry
    async def handle(m):
        messages.append(m)

    await device.start()
    await device.connection.send_message("test")

    assert messages == ["test"]

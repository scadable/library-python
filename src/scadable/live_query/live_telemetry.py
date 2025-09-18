import asyncio
from typing import Callable, Awaitable, Any
from .connection_type import ConnectionFactory, Connection


class DeviceFactory:
    """
    A class to create Devices

    Instance attributes:
        api_key: API Key to authenticate devices
        dest_url: URL of the websocket
        connection_type: WSS or WS depending on websocket type
    """

    def __init__(self, api_key: str, connection_factory: ConnectionFactory):
        self.api_key = api_key
        self.connection_factory = connection_factory

    def create_device(self, device_id: str):
        """
        Creates a device that subscribes to a websocket

        :param device_id: ID of the device we connect to
        :return: Created device
        """
        return Device(self.connection_factory.create_connection(device_id))


class Device:
    """
    A class that represents a single device

    Instance attributes:
        ws_url: fully formed websocket url that we can connect to
        raw_bus: set of subscribed handlers that will be called when receiving a response (raw)
    """

    def __init__(self, connection: Connection):
        self.connection = connection

        # Bus that contains all functions that handle raw data
        self.raw_bus: set[Callable[[str], Awaitable[Any]]] = set()

        self._stop_event = asyncio.Event()

    def raw_live_telemetry(self, subscriber: Callable[[str], Awaitable]):
        """
        Decorator that adds a function to the bus
        :param subscriber: Function that subscribes to raw data
        :return: subscriber
        """
        self.raw_bus.add(subscriber)
        return subscriber

    async def _handle_raw(self, data: str):
        """
        Internal method to prase raw data and send it to a different bus
        :param data: raw data that was received by the connection
        :return: None
        """
        await asyncio.gather(*[s(data) for s in self.raw_bus])

    async def start(self):
        """
        Starts the connection to the server to receive live telemetry
        :return: None
        """
        await self.connection.connect(self._handle_raw)

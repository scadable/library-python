import asyncio
from typing import Callable, Awaitable, Any
from websockets.asyncio import client


class DeviceFactory:
    """
    A class to create Devices

    Instance attributes:
        api_key: API Key to authenticate devices
        dest_url: URL of the websocket
        connection_type: WSS or WS depending on websocket type
    """

    def __init__(self, api_key: str, dest_url: str = "", connection_type="wss"):
        self.api_key = api_key
        self.connection_type = connection_type
        self.dest_url = dest_url

    def create_device(self, device_id: str):
        """
        Creates a device that subscribes to a websocket

        :param device_id: ID of the device we connect to
        :return: Created device
        """
        return Device(
            f"{self.connection_type}://{self.dest_url}?token={self.api_key}&deviceid={device_id}"
        )


class Device:
    """
    A class that represents a single device

    Instance attributes:
        ws_url: fully formed websocket url that we can connect to
        raw_bus: set of subscribed handlers that will be called when receiving a response (raw)
    """

    def __init__(self, wss_url: str):
        self.ws_url = wss_url

        # Bus that handles all the raw data
        self.raw_bus: set[Callable[[str], Awaitable[Any]]] = set()
        self.raw_live_telemetry(self._handle_raw)

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
        :param data: raw data that was received by the websocket
        :return: None
        """
        print(data)

    async def start(self):
        """
        Starts the websocket connection to the server to receive live telemetry
        :return: None
        """
        async with client.connect(self.ws_url) as ws:
            async for message in ws:
                await asyncio.gather(*[s(message) for s in self.raw_bus])

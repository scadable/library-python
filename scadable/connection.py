from websockets.asyncio import client
from websockets.asyncio.client import ClientConnection
from typing import Callable, Awaitable


class ConnectionFactory:  # pragma: no cover
    """
    Abstract Connection Factory

    These factories create 'Connection' types which live_telemetry will use. This is passed into the DeviceFactory
    which creates devices that we can subscribe to.

    We expose create_connection(device_id) so we can pass in an instance of any type of factory
    """

    def create_connection(self, api_key: str, device_id: str) -> "Connection":
        """
        Creates a connection to a device
        :param api_key: API key of the connection you want to create
        :param device_id: Device Id of the device
        :return: Connection
        """
        raise NotImplementedError


class WebsocketConnectionFactory(ConnectionFactory):
    """
    A factory that creates websocket connections.

    Instance Attributes:
        connection_type: ws or wss depending on the connection type
    """

    def __init__(self, dest_uri: str, connection_type="wss"):
        """
        Init for a Websocket Factory
        :param dest_uri: Destination URI of the websocket
        :param connection_type: Connection type (wss or ws)
        """
        self.connection_type = connection_type
        self._dest_uri = dest_uri

    def create_connection(self, api_key: str, device_id: str) -> "Connection":
        """
        Creates a connection to a device
        :param api_key: API key of the connection you want to create
        :param device_id: Device Id of the device
        :return: WebsocketConnection
        """
        return WebsocketConnection(
            f"{self.connection_type}://{self._dest_uri}?token={api_key}&deviceid={device_id}"
        )


class Connection:  # pragma: no cover
    """
    Abstract Connection

    A generic connection that the device uses to send and receive messages.

    We expose:
        - connect(func)
        - send_message(str)
        - stop()
    to interact with the connection.
    """

    async def connect(self, handler: Callable[[str], Awaitable]):
        """
        Connects to a server
        :param handler: Function that handles messages
        :return: None
        """
        raise NotImplementedError

    async def send_message(self, message: str):
        """
        Sends a message through the connection
        :param message: Message to be sent
        :return: None
        """
        raise NotImplementedError

    async def stop(self):
        """
        Ends the connection
        :return: None
        """
        raise NotImplementedError


class WebsocketConnection(Connection):
    """
    A class representing a Websocket Connection

    Instance Attributes:
        dest_uri: full uri of the destination, e.g. wss://localhost:8765&apikey=a&deviceid=b
    """

    def __init__(self, dest_uri: str):
        super().__init__()
        self.dest_uri = dest_uri
        self._ws: ClientConnection | None = None

    async def connect(self, handler: Callable[[str], Awaitable]):
        """
        Starts the websocket connection to the server to receive data
        :return: None
        """
        async with client.connect(self.dest_uri) as ws:
            self._ws = ws
            async for message in ws:
                await handler(message)

        self._ws = None

    async def send_message(self, message: str):
        """
        Sends a message to the websocket connection
        :param message: Message to send
        :return:
        """
        if self._ws:
            await self._ws.send(message)

    async def stop(self):
        """
        Ends the websocket connection to the server gracefully
        :return: None
        """
        if self._ws:
            await self._ws.close()

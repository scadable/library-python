import asyncio
from websockets.asyncio import client
from websockets.asyncio.client import ClientConnection
from websockets.exceptions import ConnectionClosed
from typing import Callable, Awaitable


class ConnectionFactory:
    def create_connection(self, device_id: str) -> "Connection":  # pragma: no cover
        raise NotImplementedError


class WebsocketConnectionFactory(ConnectionFactory):
    def __init__(self, dest_uri: str, api_key: str, connection_type="wss"):
        self.connection_type = connection_type
        self.dest_uri = dest_uri
        self.api_key = api_key

    def create_connection(self, device_id: str) -> "Connection":
        return WebsocketConnection(
            f"{self.connection_type}://{self.dest_uri}?token={self.api_key}&deviceid={device_id}"
        )


class Connection:
    def __init__(self):
        pass

    async def connect(self, handler: Callable[[str], Awaitable]):  # pragma: no cover
        """
        Connects to a server
        :param handler: Function that handles messages
        :return: None
        """
        raise NotImplementedError

    async def send_message(self, message: str):  # pragma: no cover
        """
        Sends a message through the connection
        :param message: Message to be sent
        :return: None
        """
        raise NotImplementedError

    async def stop(self):  # pragma: no cover
        """
        Ends the connection
        :return: None
        """
        raise NotImplementedError


class WebsocketConnection(Connection):
    def __init__(self, dest_uri: str):
        super().__init__()
        self.dest_uri = dest_uri
        self.ws: ClientConnection | None = None
        self._stop_event = asyncio.Event()

    async def connect(self, handler: Callable[[str], Awaitable]):
        """
        Starts the websocket connection to the server to receive data
        :return: None
        """
        stop_flag = False
        async for ws in client.connect(self.dest_uri):
            try:
                self.ws = ws
                async for message in ws:
                    if self._stop_event.is_set():
                        stop_flag = True
                        break
                    await handler(message)

                if stop_flag:
                    break
            except ConnectionClosed:
                continue
        self.ws = None

    async def send_message(self, message: str):
        """
        Sends a message to the websocket connection
        :param message: Message to send
        :return:
        """
        if self.ws:
            await self.ws.send(message)

    async def stop(self):
        """
        Ends the websocket connection to the server gracefully
        :return: None
        """
        self._stop_event.set()
        self.ws = None

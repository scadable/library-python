import asyncio
from websockets.asyncio import server as WeboscketServer
from scadable.connection import WebsocketConnection, WebsocketConnectionFactory
import pytest
import pytest_asyncio


async def echo_server(connection: WeboscketServer.ServerConnection):
    async for message in connection:
        await connection.send(message)


class BasicWebsocketServer:
    def __init__(self, uri="localhost", port=8765):
        self.uri = uri
        self.port = port

        self.handler = echo_server
        self.server: WeboscketServer.Server | None = None

    def full_uri(self):
        return f"{self.uri}:{self.port}"

    async def _handle(self, connection):
        if self.handler:
            await self.handler(connection)

    def set_handler(self, handler):
        self.handler = handler

    async def start(self):
        if self.server:
            await self.stop()

        self.server = await WeboscketServer.serve(self._handle, self.uri, self.port)

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None


@pytest_asyncio.fixture(scope="session")
async def websocket_server():
    server = BasicWebsocketServer()
    yield server


@pytest.mark.asyncio
async def test_ws_connection_factory(websocket_server):
    factory = WebsocketConnectionFactory(
        dest_uri=websocket_server.full_uri(), connection_type="ws"
    )
    assert factory._dest_uri == websocket_server.full_uri()
    assert factory.connection_type == "ws"

    conn = factory.create_connection("apikey", "deviceid")
    assert isinstance(conn, WebsocketConnection)
    assert (
            conn.dest_uri
            == f"ws://{websocket_server.full_uri()}?token=apikey&deviceid=deviceid"
    )


@pytest.mark.asyncio
async def test_connection(websocket_server):
    await websocket_server.start()
    factory = WebsocketConnectionFactory(
        dest_uri=websocket_server.full_uri(), connection_type="ws"
    )
    conn = factory.create_connection("apikey", "deviceid")

    echo_messages = []

    async def handler(message):
        echo_messages.append(message)
        await conn.stop()

    async def run():
        await asyncio.sleep(1)
        await conn.send_message("test")

    await asyncio.gather(conn.connect(handler), run())

    assert echo_messages == ["test"]

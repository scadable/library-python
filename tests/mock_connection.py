from scadable.connection import ConnectionFactory, Connection


class TestConnectionFactory(ConnectionFactory):
    __test__ = False

    def create_connection(self, api_key, device_id):
        return TestConnection()


class TestConnection(Connection):
    __test__ = False

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

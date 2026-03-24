from __future__ import annotations

from ._config import ClientConfig
from ._transport._http import SyncHTTPTransport, AsyncHTTPTransport
from ._transport._websocket import WebSocketTransport
from ._resources._gateways import Gateways, AsyncGateways


class Scadable:
    """Synchronous Scadable client.

    >>> client = Scadable(api_key="sk_live_...")
    >>> for gw in client.gateways.list():
    ...     print(gw.name, gw.status)
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ):
        self._config = ClientConfig.resolve(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._transport = SyncHTTPTransport(self._config)

        self.gateways = Gateways(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> Scadable:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncScadable:
    """Asynchronous Scadable client with streaming support.

    >>> client = AsyncScadable(api_key="sk_live_...")
    >>> async with client.gateways.stream("gw-123") as stream:
    ...     async for event in stream:
    ...         print(event.data)
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ):
        self._config = ClientConfig.resolve(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._transport = AsyncHTTPTransport(self._config)
        self._ws_transport = WebSocketTransport(self._config)

        self.gateways = AsyncGateways(self._transport, self._ws_transport)

    async def close(self) -> None:
        await self._transport.close()
        await self._ws_transport.close()

    async def __aenter__(self) -> AsyncScadable:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

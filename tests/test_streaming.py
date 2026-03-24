import pytest

from scadable._resources._gateways import AsyncGateways
from scadable._transport._http import AsyncHTTPTransport
from scadable._config import ClientConfig


@pytest.mark.asyncio
async def test_stream_requires_async_client():
    """Streaming without a stream transport should raise RuntimeError."""
    config = ClientConfig(api_key="sk_test", base_url="https://test.scadable.com")
    gateways = AsyncGateways(AsyncHTTPTransport(config), stream_transport=None)
    with pytest.raises(RuntimeError, match="Streaming requires AsyncScadable"):
        async with gateways.stream(project_id="p1", gateway_id="gw1"):
            pass


def test_websocket_transport_init():
    """WebSocketTransport should initialize without error."""
    from scadable._transport._websocket import WebSocketTransport

    config = ClientConfig(api_key="sk_test", base_url="https://app.scadable.com")
    transport = WebSocketTransport(config)
    assert transport._config.api_key == "sk_test"

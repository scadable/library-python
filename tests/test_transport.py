import pytest
import respx
from httpx import Response

from scadable._config import ClientConfig
from scadable._transport._http import SyncHTTPTransport, AsyncHTTPTransport
from scadable._exceptions import (
    AuthenticationError,
    ConnectionError,
    InternalServerError,
    RateLimitError,
)


@pytest.fixture
def config():
    return ClientConfig(
        api_key="sk_test",
        base_url="https://test.scadable.com",
        timeout=5.0,
        max_retries=1,
    )


def test_sync_success(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(200, json={"ok": True}))
        transport = SyncHTTPTransport(config)
        resp = transport.request("GET", "/api/test")
        assert resp.status_code == 200
        assert resp.data == {"ok": True}
        transport.close()


def test_sync_retry_on_500(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(
            side_effect=[
                Response(500, json={"error": "oops"}),
                Response(200, json={"ok": True}),
            ]
        )
        transport = SyncHTTPTransport(config)
        resp = transport.request("GET", "/api/test")
        assert resp.status_code == 200
        transport.close()


def test_sync_retry_exhausted_500(config):
    config.max_retries = 0
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(500, json={"error": "down"}))
        transport = SyncHTTPTransport(config)
        with pytest.raises(InternalServerError):
            transport.request("GET", "/api/test")
        transport.close()


def test_sync_429_raises_rate_limit(config):
    config.max_retries = 0
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(
            return_value=Response(429, json={"error": "rate limited"})
        )
        transport = SyncHTTPTransport(config)
        with pytest.raises(RateLimitError):
            transport.request("GET", "/api/test")
        transport.close()


def test_sync_non_json_response(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(200, text="OK"))
        transport = SyncHTTPTransport(config)
        resp = transport.request("GET", "/api/test")
        assert resp.status_code == 200
        transport.close()


def test_sync_non_json_error(config):
    config.max_retries = 0
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(401, text="Unauthorized"))
        transport = SyncHTTPTransport(config)
        with pytest.raises(AuthenticationError):
            transport.request("GET", "/api/test")
        transport.close()


@pytest.mark.asyncio
async def test_async_success(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(200, json={"ok": True}))
        transport = AsyncHTTPTransport(config)
        resp = await transport.request("GET", "/api/test")
        assert resp.status_code == 200
        assert resp.data == {"ok": True}
        await transport.close()


@pytest.mark.asyncio
async def test_async_retry_on_500(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(
            side_effect=[
                Response(500, json={"error": "oops"}),
                Response(200, json={"ok": True}),
            ]
        )
        transport = AsyncHTTPTransport(config)
        resp = await transport.request("GET", "/api/test")
        assert resp.status_code == 200
        await transport.close()


@pytest.mark.asyncio
async def test_async_retry_exhausted(config):
    config.max_retries = 0
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(500, json={"error": "down"}))
        transport = AsyncHTTPTransport(config)
        with pytest.raises(InternalServerError):
            await transport.request("GET", "/api/test")
        await transport.close()


def test_sync_with_params(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.get("/api/test").mock(return_value=Response(200, json=[]))
        transport = SyncHTTPTransport(config)
        resp = transport.request("GET", "/api/test", params={"range": "1h"})
        assert resp.status_code == 200
        transport.close()


def test_sync_with_json_body(config):
    with respx.mock(base_url="https://test.scadable.com") as mock:
        mock.post("/api/test").mock(return_value=Response(201, json={"id": "new"}))
        transport = SyncHTTPTransport(config)
        resp = transport.request("POST", "/api/test", json={"name": "test"})
        assert resp.status_code == 201
        transport.close()
